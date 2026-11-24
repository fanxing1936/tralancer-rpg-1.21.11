$data modify storage rpg:paradise r.p$(id).dim set from entity @s Dimension
$execute store result storage rpg:paradise r.p$(id).x double 0.01 run data get entity @s Pos[0] 100
$execute store result storage rpg:paradise r.p$(id).y double 0.01 run data get entity @s Pos[1] 100
$execute store result storage rpg:paradise r.p$(id).z double 0.01 run data get entity @s Pos[2] 100
$execute store result storage rpg:paradise r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100
