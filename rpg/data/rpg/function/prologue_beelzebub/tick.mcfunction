# 别西卜（序章）每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[tag=rpg.pr.w.beelzebub,tag=!rpg.prbz,limit=1] as @e[tag=rpg.pr.w.beelzebub,tag=!rpg.prbz] at @s run function rpg:prologue_beelzebub/dress
execute if entity @e[tag=rpg.prbz,limit=1] as @e[tag=rpg.prbz] at @s run function rpg:prologue_beelzebub/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.prbz.part,predicate=!rpg:prologue_beelzebub/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.prbz.part,predicate=!rpg:prologue_beelzebub/riding]
