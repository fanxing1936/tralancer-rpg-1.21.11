execute if score @s rpg_mk_life matches 13 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,1.2f,4.5f]}}
execute if score @s rpg_mk_life matches 12 run data modify entity @s text.text set value ""
execute if score @s rpg_mk_life matches 10 run data modify entity @s text.text set value ""
execute if score @s rpg_mk_life matches 8 run data modify entity @s text.text set value ""
execute if score @s rpg_mk_life matches 6 run data modify entity @s text.text set value ""
execute if score @s rpg_mk_life matches 4 run data modify entity @s text.text set value ""
