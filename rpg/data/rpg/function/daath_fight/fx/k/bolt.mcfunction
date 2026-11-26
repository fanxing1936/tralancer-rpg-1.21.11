execute if score @s rpg_dt_life matches 3 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[0.01f,12f,0.01f]}}
execute if score @s rpg_dt_life matches 8 run data modify entity @s text.text set value ""
execute if score @s rpg_dt_life matches 6 run data modify entity @s text.text set value ""
execute if score @s rpg_dt_life matches 4 run data modify entity @s text.text set value ""
