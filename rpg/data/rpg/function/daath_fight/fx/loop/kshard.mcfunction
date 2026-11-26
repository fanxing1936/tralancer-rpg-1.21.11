scoreboard players operation #f rpg_dt_life = @s rpg_dt_life
scoreboard players set #fk rpg_dt_life 3
scoreboard players operation #g rpg_dt_life = #f rpg_dt_life
scoreboard players operation #g rpg_dt_life %= #fk rpg_dt_life
execute unless score #g rpg_dt_life matches 0 run return 0
scoreboard players operation #f rpg_dt_life /= #fk rpg_dt_life
scoreboard players set #fk rpg_dt_life 4
scoreboard players operation #f rpg_dt_life %= #fk rpg_dt_life
execute if score #f rpg_dt_life matches 0 run return run data modify entity @s text.text set value ""
execute if score #f rpg_dt_life matches 1 run return run data modify entity @s text.text set value ""
execute if score #f rpg_dt_life matches 2 run return run data modify entity @s text.text set value ""
execute if score #f rpg_dt_life matches 3 run return run data modify entity @s text.text set value ""
