execute on passengers if entity @s[tag=rpg.lu.part] run rotate @s ~ 0
execute if entity @s[tag=rpg.exorcism.bound,tag=!rpg.lu.bound] run function rpg:lucifer_lord/bound/start
execute unless entity @s[tag=rpg.exorcism.bound] if entity @s[tag=rpg.lu.bound] run function rpg:lucifer_lord/bound/end
scoreboard players add @s rpg_lu_clock 1
execute if score @s rpg_lu_clock matches 4.. run function rpg:lucifer_lord/movement/check
execute if score @s rpg_lu_clock matches 4.. run scoreboard players set @s rpg_lu_clock 0
function rpg:lucifer_lord/anim/tick
execute store result score @s rpg_lu_hurt run data get entity @s HurtTime
execute if score @s rpg_lu_hurt matches 10 run function rpg:lucifer_lord/sound/hurt
execute if predicate rpg:lucifer_lord/ambient run function rpg:lucifer_lord/sound/idle
