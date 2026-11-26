# leggings（as 载体）
execute on passengers if entity @s[tag=rpg.dtm.s.legs] run item replace entity @s contents from entity @a[tag=rpg.dt.me,limit=1] armor.legs
execute on passengers if entity @s[tag=rpg.dtm.s.legs] run function rpg:daath/wear/fit_legs
