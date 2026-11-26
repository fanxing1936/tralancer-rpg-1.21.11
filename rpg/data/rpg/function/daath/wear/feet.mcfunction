# boots（as 载体）
execute on passengers if entity @s[tag=rpg.dtm.s.feet] run item replace entity @s contents from entity @a[tag=rpg.dt.me,limit=1] armor.feet
execute on passengers if entity @s[tag=rpg.dtm.s.feet] run function rpg:daath/wear/fit_feet
