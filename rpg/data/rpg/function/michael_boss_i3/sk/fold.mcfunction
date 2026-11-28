execute if score @s rpg_mk_t matches 1..38 run particle minecraft:end_rod ~ ~1.3 ~ 0.4 0.7 0.4 0.01 1
execute if score @s rpg_mk_t matches 2 run function rpg:michael_boss_i3/fold/close
execute if score @s rpg_mk_t matches 30 run playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.4
execute if score @s rpg_mk_t matches 40 run function rpg:michael_boss_i3/fold/open
execute if score @s rpg_mk_t matches 62.. run function rpg:michael_boss_i3/sk/end
