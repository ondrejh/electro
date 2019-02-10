<!DOCTYPE HTML>
	
<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Spotřeba elektrické nergie</title>
	<link rel="stylesheet" type="text/css" href="files/style.css" media="screen" />
	<link rel="shortcut icon" href="files/energy.ico" />

	<link rel="stylesheet" href="files/lightbox.css">

	<script src="files/jquery-1.11.0.min.js"></script>
	<script src="files/lightbox.js"></script>

</head>

<body>

<section id=main>
<article>

<header>
<img class="full" src="files/wattmeter.jpg" alt="ftipny obrazek">
</header>

<h2>Denní graf spotřeby elektrické energie</h2>
<p>
	<!-- graf spotreby -->

	<figure class="center">
		<?php
			$dir = 'energy_data';
			$files = scandir($dir);
			$wfiles = [];
			foreach ($files as $filename) {
				if (substr_compare($filename,'_wattage',8,8)===0)
					$wfiles[] = $filename;
			}
			$len = count($wfiles);
			$cnt = 0;
			foreach ($wfiles as $filename) {
				echo "<a href=\"energy_data/";
				print($filename);
				$cnt = $cnt+1;
				if ($cnt<$len)
					echo "\" data-lightbox=\"roadtrip\"></a>\n";
				else {
					echo "\" data-lightbox=\"roadtrip\"><img class=\"fill\" src=\"energy_data/";
					print($filename);
					echo "\" alt=\"graf spotřeby elektrické energie\">\n";
					echo "<figcaption>Graf spotřeby elektřiny (klikni pro galerii starších grafů)</figcaption></a>";
				}
			}
		?>
		<!--<a href="energy_data/dummy2.png" data-lightbox="roadtrip"></a>
		<a href="energy_data/dummy1.png" data-lightbox="roadtrip"></a>
		<a href="energy_data/dummy0.png" data-lightbox="roadtrip"><img class="full" src="energy_data/dummy0.png" alt="graf spotřeby elektřiny">
		<figcaption>Graf spotřeby elektřiny (klikni pro galerii starších grafů)</figcaption></a>-->
	</figure>

	<!-- konec graf spotreby -->
</p>

</article>
</section><!--main-->

</body>

</html>
