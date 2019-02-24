<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <meta name="rating" content="general">
    <meta name="author" content="ondrejh">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Elektroměr</title>
    <meta name="description" content="Zobrazení dat z elektroměru." />
    <meta name="keywords" content="elektroměr" />

    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/4.0.0/normalize.min.css" media="screen, print" />
    <link rel="stylesheet" type="text/css" href="style.css" media="screen, print" />
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic|Oswald&amp;subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <link rel="shortcut icon" href="favicon.ico" />
    <script src="plotly-latest.min.js"></script>
</head>

<body class="home">

    <header id="top">
        <h1>Elektroměr</h1>
    </header>

    <section class="content">

        <article class="main">
            <div id='chart'></div>

            <?php // get data
                function get_kwh($one_tariff_reading) {
                    $ar1 = explode("*kWh", explode("1.8.0(", $one_tariff_reading, 2)[1], 2);
                    $ar2 = explode("*kWh", explode("1.8.1(", $ar1[1], 2)[1], 2);
                    $ar3 = explode("*kWh", explode("1.8.2(", $ar2[1], 2)[1], 2);
                    
                    $tot_kwh = $ar1[0];
                    $t1_kwh = $ar2[0];
                    $t2_kwh = $ar3[0];
                    
                    return array($tot_kwh, $t1_kwh, $t2_kwh);
                }
            
                $db = new SQLite3("/home/pi/data/tariff.sql");
                
                $query = "SELECT MAX(timestamp) FROM readings";
                $db_data = $db->query($query);
                $maxts = $db_data->fetchArray()[0];
                $query = "SELECT body FROM readings WHERE timestamp='{$maxts}'";//ORDER BY timestamp";
                $db_data = $db->query($query);
                $body = $db_data->fetchArray()[0];
                //echo "<p>{$maxts}<br>{$body}</p>";
            
                $p = get_kwh($body);
            
                //echo "<p>Total: {$p[0]} kWh<br>Tariff 1: {$p[1]} kWh<br>Tariff 2: {$p[2]} kWh</p>". PHP_EOL. PHP_EOL;
            
                //echo "</article></section></body></html>";
                //exit();
            
                $maxts_minus = date("Y-m-d H:i", strtotime('-3 day', strtotime($maxts)));
                $query = "SELECT timestamp, body FROM readings WHERE timestamp > '{$maxts_minus}' ORDER BY timestamp";
                $db_data = $db->query($query);
                $entries = array();
                while($row = $db_data->fetchArray()) {
                    $p = get_kwh($row['body']);
                    $entries[] = array(date("Y-m-d H:i", strtotime($row['timestamp'])), floatval($p[0]), floatval($p[1]), floatval($p[2]));
                }
                $watage = array();
                $first = true;
                $tT = 0.0;
                $t1 = 0.0;
                $t2 = 0.0;
                $ts = "";

                #$watL = array();
                $watHcnt = -1;
                $watLcnt = -1;
                $watH = array();
                $watL = array();
                $changes = array();
                $tarif = 'none';
                $cnt = 0;
                $lw = 0.0;
                $lw1 = 0.0;
                $lw2 = 0.0;
                //echo "<p><table><tr><th>Time</th><th>Total [kWh]</th><th>Tariff 1 [kWh]</th><th>Tariff 2 [kWh]</th></tr>". PHP_EOL;
                foreach ($entries as $e) {
                    if ($first) {
                        $first = false;
                    }
                    else {
                        $dt = (strtotime($e[0]) - strtotime($ts)) / 3600;
                        $wT = ($e[1] - $tT) / $dt;
                        $w1 = ($e[2] - $t1) / $dt;
                        $w2 = ($e[3] - $t2) / $dt;
                        $watage[] = array($e[0], $wT, $w1, $w2);
                        
                        if (($lw1 == 0.0) && ($w1 != 0.0)) {
                            if ($tarif != 'high') {
                                $tarif = 'high';
                                $watHcnt += 1;
                                $watH[] = array();
                                $pt = $dt / ($e[1] - $tT) * ($e[2] - $t1);
                                #echo $pt. " = ". $dt. " / (". $e[1]. " - ". $tT. ") * (". $e[2]. " - ". $t1. ")<br>";
                                $t = date("Y-m-d H:i", strtotime("+". round($pt*3600). " seconds", strtotime($ts)));
                                #echo $t. " = ". $ts. " + ". $pt. "h<br>";
                                $w = $lw + ($wT - $lw) / $dt * $pt;
                                $changes[] = array($t, $w);
                                #echo $pt. " .. ". $t. " .. ". $w. "<br>";
                                if ($watLcnt >= 0)
                                    $watL[$watLcnt][$cnt] = array($t, $w);
                                $watH[$watHcnt][0] = array($t, $w);
                                $cnt = 1;
                            }
                        }
                        else if (($lw2 == 0.0) && ($w2 != 0.0)) {
                            if ($tarif != 'low') {
                                $tarif = 'low';
                                $watLcnt += 1;
                                $watL[] = array();
                                $pt = $dt / ($e[1] - $tT) * ($e[3] - $t2);
                                #echo $pt. " = ". $dt. " / (". $e[1]. " - ". $tT. ") * (". $e[3]. " - ". $t2. ")<br>";
                                $t = date("Y-m-d H:i", strtotime("+". round($pt*3600). " seconds", strtotime($ts)));
                                $w = $lw + ($wT - $lw) / $dt * $pt;
                                $changes[] = array($t, $w);
                                #echo $t. " .. ". $w. "<br>";
                                if ($watHcnt >= 0)
                                    $watH[$watHcnt][$cnt] = array($t, $w);
                                $watL[$watLcnt][0] = array($t, $w);
                                $cnt = 1;
                            }
                        }
                        
                        if ($tarif === 'high') {
                            $watH[$watHcnt][$cnt] = array($e[0], $wT);
                            $cnt += 1;
                        }
                        else if ($tarif === 'low') {
                            $watL[$watLcnt][$cnt] = array($e[0], $wT);
                            $cnt += 1;
                        }
                        
                        $lw = $wT;
                        $lw1 = $w1;
                        $lw2 = $w2;
                    }
                    $ts = $e[0];
                    $tT = $e[1];
                    $t1 = $e[2];
                    $t2 = $e[3];
                    //echo "<tr><td>{$e[0]}</td><td>{$e[1]}</td><td>{$e[2]}</td><td>{$e[3]}</td></tr>". PHP_EOL;
                }
                //echo "</table></p>";
                
                //echo "</article></section></body></html>";
                //exit();
            ?>
            
            <script>
                var tHcol = '#B21B04';
                var tLcol = '#009933';
                var tCcol = '#3333ff';
                <?php
                $cnt = 0;
                foreach ($watH as $w) {
                    echo "var tH". $cnt. " = {x: [";
                    $cnt += 1;
                    $first = true;
                    foreach ($w as $e) {
                        if ($first) $first = false;
                        else echo ', ';
                        echo "'". $e[0]. "'";
                    }
                    echo "], y: [";
                    $first = true;
                    foreach ($w as $e) {
                        if ($first) $first = false;
                        else echo ', ';
                        echo $e[1];
                    }
                    echo "], name: 'Drahý [kW]', type: 'scatter', mode: 'lines', fill: 'tozeroy', line: {color: tHcol}};". PHP_EOL;
                };
                $cnt = 0;
                foreach ($watL as $w) {
                    echo "var tL". $cnt. " = {x: [";
                    $cnt += 1;
                    $first = true;
                    foreach ($w as $e) {
                        if ($first) $first = false;
                        else echo ', ';
                        echo "'". $e[0]. "'";
                    }
                    echo "], y: [";
                    $first = true;
                    foreach ($w as $e) {
                        if ($first) $first = false;
                        else echo ', ';
                        echo $e[1];
                    }
                    echo "], name: 'Levný [kW]', type: 'scatter', mode: 'lines', fill: 'tozeroy', line: {color: tLcol}};". PHP_EOL;
                };
                echo "var tC = {x: [";
                $first = true;
                foreach ($changes as $c) {
                    if ($first) $first = false;
                    else echo ', ';
                    echo "'". $c[0]. "'";
                }
                echo "], y: [";
                $first = true;
                foreach ($changes as $c) {
                    if ($first) $first = false;
                    else echo ', ';
                    echo $c[1];
                }
                echo "], name: 'Změny [kW]', type: 'scatter', mode: 'markers', line: {color: tCcol}};". PHP_EOL;
                echo "var data = [";
                $cnt = 0;
                foreach ($watH as $w) {
                    if ($cnt) echo ", ";
                    echo "tH". $cnt;
                    $cnt += 1;
                }
                $cnt = 0;
                foreach ($watL as $w) {
                    echo ", tL". $cnt;
                    $cnt += 1;
                }
                echo "];". PHP_EOL;
                #echo ", tC];". PHP_EOL;
                ?>
                var layout = {
                    yaxis: {
                        title: 'Příkon [kW]'
                    },
                    margin: { t: 0},
                    showlegend: false
                };
                Plotly.newPlot('chart', data, layout);
            </script>
        </article>
    </section>
</body>
</html>
