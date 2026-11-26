# chestplate（as 载体）
execute on passengers if entity @s[tag=rpg.dtm.s.chest] run item replace entity @s contents from entity @a[tag=rpg.dt.me,limit=1] armor.chest
execute on passengers if entity @s[tag=rpg.dtm.s.chest] run function rpg:daath/wear/fit_chest
