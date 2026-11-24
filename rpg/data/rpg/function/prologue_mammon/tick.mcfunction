# 玛门（序章）每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.mammon,tag=!rpg.prmm,limit=1] as @e[tag=rpg.pr.w.mammon,tag=!rpg.prmm] at @s run function rpg:prologue_mammon/dress
execute if entity @e[tag=rpg.prmm,limit=1] as @e[tag=rpg.prmm] at @s run function rpg:prologue_mammon/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prmm.part,predicate=!rpg:prologue_mammon/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prmm.part,predicate=!rpg:prologue_mammon/riding]
