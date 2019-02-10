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
            
                $maxts_minus_2days = date("Y-m-d H:i", strtotime('-2 day', strtotime($maxts)));
                $query = "SELECT timestamp, body FROM readings WHERE timestamp > '{$maxts_minus_2days}' ORDER BY timestamp";
                $db_data = $db->query($query);
                $entries = array();
                while($row = $db_data->fetchArray()) {
                    $p = get_kwh($row['body']);
                    $entries[] = array(date("Y-m-d H:i", strtotime($row['timestamp'])), floatval($p[0]), floatval($p[1]), floatval($p[2]));
                }
                $watage = array();
                $first = true;
                $t = 0.0;
                $t1 = 0.0;
                $t2 = 0.0;
                //echo "<p><table><tr><th>Time</th><th>Total [kWh]</th><th>Tariff 1 [kWh]</th><th>Tariff 2 [kWh]</th></tr>". PHP_EOL;
                foreach ($entries as $e) {
                    if ($first) {
                        $first = false;
                    }
                    else {
                        $w = $e[1] - $t;
                        $w1 = $e[2] - $t1;
                        $w2 = $e[3] - $t2;
                        $watage[] = array($e[0], $w, $w1, $w2);
                    }
                    $t = $e[1];
                    $t1 = $e[2];
                    $t2 = $e[3];
                    //echo "<tr><td>{$e[0]}</td><td>{$e[1]}</td><td>{$e[2]}</td><td>{$e[3]}</td></tr>". PHP_EOL;
                }
                //echo "</table></p>";
                
                //echo "</article></section></body></html>";
                //exit();
            ?>
            
            <script>
                var t1col = '#DDDDDD';
                var t2col = '#B21B04';
                var t3col = '#2E4AA9';
                var trace1 = {
                    x: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            #echo "'". date('Y-m-d H:i:s', strtotime($e[0])). "'";
                            echo "'". $e[0]. "'";
                        }
                        ?>],
                    y: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            echo $e[1];
                        }
                        ?>],
                    name: 'Celkem [kW]',
                    type: 'scatter',
                    line: {
                        color: t1col
                    }
                };
                var trace2 = {
                    x: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            #echo "'". date('Y-m-d H:i:s', strtotime($e[0])). "'";
                            echo "'". $e[0]. "'";
                        }
                        ?>],
                    y: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            echo $e[2];
                        }
                        ?>],
                    name: 'Drahý [kW]',
                    type: 'scatter',
                    line: {
                        color: t2col
                    }
                };
                var trace3 = {
                    x: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            #echo "'". date('Y-m-d H:i:s', strtotime($e[0])). "'";
                            echo "'". $e[0]. "'";
                        }
                        ?>],
                    y: [<?php
                        $first = true;
                        foreach ($watage as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            echo $e[3];
                        }
                        ?>],
                    name: 'Levný [kW]',
                    type: 'scatter',
                    line: {
                        color: t3col
                    }
                };
                var data = [trace1, trace2, trace3];
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
