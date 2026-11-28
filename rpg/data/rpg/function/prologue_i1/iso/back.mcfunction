$gamemode $(gm) @s
$experience set @s $(xl) levels
$experience set @s $(xp) points
$execute in $(dim) run tp @s $(x) $(y) $(z) $(yaw) 0
effect give @s minecraft:instant_health 1 4 true
