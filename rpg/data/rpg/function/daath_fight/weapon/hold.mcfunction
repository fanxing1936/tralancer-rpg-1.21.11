execute store result score @s rpg_dt_wc run data get storage rpg:daath t.cur.c
execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run data modify entity @s item set from storage rpg:daath t.cur.item
execute if score @s rpg_dt_wc matches 6 on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data modify entity @s item set from storage rpg:daath t.cur.item
execute unless score @s rpg_dt_wc matches 6 on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data remove entity @s item
particle minecraft:smoke ^-0.4 ^1.1 ^0.4 0.1 0.2 0.1 0.01 4
