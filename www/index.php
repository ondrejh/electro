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
            <h2>Poslední odečet</h2>
            <p>
            <div id='last_reading_timestamp'>1.1.1111 22:22</div>
            T1:<div id='last_reading_t1'>0.000</div>kWh
            T2:<div id='last_reading_t2'>0.000</div>kWh
            Celkem:<div id='last_reading_ttot'>0.000</div>kWh </p>
            <h2>Spotřeba energie za poslední 3 dny</h2>
            <div id='chart'></div>

            <?php // get data php section
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

            $lastp = get_kwh($body);

            $maxts_minus = date("Y-m-d H:i", strtotime('-3 day', strtotime($maxts)));
            $query = "SELECT timestamp, body FROM readings WHERE timestamp > '{$maxts_minus}' ORDER BY timestamp";
            $db_data = $db->query($query);
            $entries = array();
            while($row = $db_data->fetchArray()) {
                $p = get_kwh($row['body']);
                $entries[] = array(date("Y-m-d H:i", strtotime($row['timestamp'])), floatval($p[0]), floatval($p[1]), floatval($p[2]));
            }

            $first = true;
            $tT = 0.0;
            $t1 = 0.0;
            $t2 = 0.0;
            $ts = "";

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

            foreach ($entries as $e) {
                if ($first) {
                    $first = false;
                }
                else {
                    # calculate current watages
                    $dt = (strtotime($e[0]) - strtotime($ts)) / 3600;
                    $wT = ($e[1] - $tT) / $dt; # total
                    $w1 = ($e[2] - $t1) / $dt; # high
                    $w2 = ($e[3] - $t2) / $dt; # low

                    # test tarif changes
                    if (($lw1 == 0.0) && ($w1 != 0.0)) {
                        if ($tarif != 'high') {
                            # switch tarif
                            $tarif = 'high';
                            # create new high tarif line
                            $watHcnt += 1;
                            $watH[] = array();
                            # calculate time when tarif changed
                            $pt = $dt / ($e[1] - $tT) * ($e[2] - $t1);
                            $t = date("Y-m-d H:i", strtotime("+". round($pt*3600). " seconds", strtotime($ts)));
                            # aproximate watage at the change time
                            $w = $lw + ($wT - $lw) / $dt * $pt;
                            # save into chagnes array
                            $changes[] = array($t, $w);
                            # add value into end of previous and begin of new line
                            if ($watLcnt >= 0)
                                $watL[$watLcnt][$cnt] = array($t, round($w, 3));
                            $watH[$watHcnt][0] = array($t, round($w, 3));
                            $cnt = 1;
                        }
                    }
                    else if (($lw2 == 0.0) && ($w2 != 0.0)) {
                        if ($tarif != 'low') {
                            # switch tarif
                            $tarif = 'low';
                            # create new high tarif line
                            $watLcnt += 1;
                            $watL[] = array();
                            # calculate time when tarif changed
                            $pt = $dt / ($e[1] - $tT) * ($e[3] - $t2);
                            $t = date("Y-m-d H:i", strtotime("+". round($pt*3600). " seconds", strtotime($ts)));
                            # aproximate watage at the change time
                            $w = $lw + ($wT - $lw) / $dt * $pt;
                            # save into chagnes array
                            $changes[] = array($t, $w);
                            # add value into end of previous and begin of new line
                            if ($watHcnt >= 0)
                                $watH[$watHcnt][$cnt] = array($t, round($w, 3));
                            $watL[$watLcnt][0] = array($t, round($w, 3));
                            $cnt = 1;
                        }
                    }

                    # add value into current line
                    if ($tarif === 'high') {
                        $watH[$watHcnt][$cnt] = array($e[0], $wT);
                        $cnt += 1;
                    }
                    else if ($tarif === 'low') {
                        $watL[$watLcnt][$cnt] = array($e[0], $wT);
                        $cnt += 1;
                    }

                    #save value for the next calculation
                    $lw = $wT;
                    $lw1 = $w1;
                    $lw2 = $w2;
                }
                $ts = $e[0];
                $tT = $e[1];
                $t1 = $e[2];
                $t2 = $e[3];
            }
            /* end of get data php */ ?>
        
            <script>
                document.getElementById("last_reading_timestamp").innerText = <?php echo "'". $maxts. "'"; ?>;
                document.getElementById("last_reading_t1").innerText = <?php echo "'". round($lastp[1], 3). "'"; ?>;
                document.getElementById("last_reading_t2").innerText = <?php echo "'". round($lastp[2], 3). "'"; ?>;
                document.getElementById("last_reading_ttot").innerText = <?php echo "'". round($lastp[0], 3). "'"; ?>;

                var tHcol = '#B21B04';
                var tLcol = '#009933';
                var tCcol = '#3333ff';
                <?php

                // tarif high data lines
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

                // tarif low data lines
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

                // changes data lines (dots)
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

                // list of all data lines to plot
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
                echo "];". PHP_EOL; // no changes dots
                #echo ", tC];". PHP_EOL; // with chages dots
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
