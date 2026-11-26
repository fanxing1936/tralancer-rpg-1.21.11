scoreboard players set @s rpg_dt_wc 0
execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run data remove entity @s item
execute on passengers if entity @s[tag=rpg.dtm.p.weapon_l] run data remove entity @s item
