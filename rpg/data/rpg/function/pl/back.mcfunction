tag @s remove rpg.pl.in
scoreboard players set @s rpg_pl_lv 0
execute store result storage rpg:paradise t.id int 1 run scoreboard players get @s rpg_fg_id
function rpg:pl/back_m with storage rpg:paradise t
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.2 1.4
