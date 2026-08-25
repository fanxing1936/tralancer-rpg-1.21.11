execute store result score #name_hurt rpg_ex_tmp run data get entity @s HurtTime 1
execute if score #name_hurt rpg_ex_tmp matches 1.. if entity @s[tag=rpg.counter.true] run return run function rpg:inquest/counter/name_true
execute if score #name_hurt rpg_ex_tmp matches 1.. if entity @s[tag=rpg.counter.false] run return run function rpg:inquest/counter/name_false
