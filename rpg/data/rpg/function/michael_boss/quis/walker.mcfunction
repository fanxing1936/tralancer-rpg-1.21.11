# 骨刺的行走点（at 起点，朝这条线）：每刻往前 1 格，破土一节
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.walker"]}
execute as @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 17
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
playsound minecraft:block.bone_block.break hostile @a[distance=..32] ~ ~ ~ 1.2 0.5
playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 0.8 0.8
