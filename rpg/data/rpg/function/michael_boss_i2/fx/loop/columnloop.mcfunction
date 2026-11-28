scoreboard players operation #f rpg_mk_life = @s rpg_mk_life
scoreboard players set #fk rpg_mk_life 2
scoreboard players operation #g rpg_mk_life = #f rpg_mk_life
scoreboard players operation #g rpg_mk_life %= #fk rpg_mk_life
execute unless score #g rpg_mk_life matches 0 run return 0
scoreboard players operation #f rpg_mk_life /= #fk rpg_mk_life
scoreboard players set #fk rpg_mk_life 6
scoreboard players operation #f rpg_mk_life %= #fk rpg_mk_life
execute if score #f rpg_mk_life matches 0 run return run data modify entity @s text.text set value ""
execute if score #f rpg_mk_life matches 1 run return run data modify entity @s text.text set value ""
execute if score #f rpg_mk_life matches 2 run return run data modify entity @s text.text set value ""
execute if score #f rpg_mk_life matches 3 run return run data modify entity @s text.text set value ""
execute if score #f rpg_mk_life matches 4 run return run data modify entity @s text.text set value ""
execute if score #f rpg_mk_life matches 5 run return run data modify entity @s text.text set value ""
