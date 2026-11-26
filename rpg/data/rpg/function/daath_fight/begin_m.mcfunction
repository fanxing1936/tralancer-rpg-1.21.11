$scoreboard players set #b$(n) rpg_dt 1
$execute store result score #sid$(n) rpg_dt run scoreboard players get @s rpg_dt_sid
$scoreboard players set #em$(n) rpg_dt 0
$data modify storage rpg:daath r.p$(id).dim set from entity @s Dimension
$execute store result storage rpg:daath r.p$(id).x double 0.01 run data get entity @s Pos[0] 100
$execute store result storage rpg:daath r.p$(id).y double 0.01 run data get entity @s Pos[1] 100
$execute store result storage rpg:daath r.p$(id).z double 0.01 run data get entity @s Pos[2] 100
$execute store result storage rpg:daath r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100
$execute if dimension rpg:daath run data modify storage rpg:daath r.p$(id) set value {dim:"minecraft:overworld",x:0.0d,y:120.0d,z:0.0d,yaw:0.0f}
$data modify storage rpg:daath s$(n) set value {arms:[]}
function rpg:daath_fight/slot/load
