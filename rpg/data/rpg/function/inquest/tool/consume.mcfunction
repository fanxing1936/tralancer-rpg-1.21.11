execute store result score #tool_count rpg_ex_tmp run data get entity @s Item.count 1
scoreboard players remove #tool_count rpg_ex_tmp 1
execute if score #tool_count rpg_ex_tmp matches 1.. store result entity @s Item.count int 1 run scoreboard players get #tool_count rpg_ex_tmp
execute if score #tool_count rpg_ex_tmp matches ..0 run kill @s
