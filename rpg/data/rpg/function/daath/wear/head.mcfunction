# helmet（as 载体）
execute on passengers if entity @s[tag=rpg.dtm.s.head] run item replace entity @s contents from entity @a[tag=rpg.dt.me,limit=1] armor.head
execute on passengers if entity @s[tag=rpg.dtm.s.head] run function rpg:daath/wear/fit_head
