# 当前 @s 是这一刻真正受伤的实体。先清旧存档或中断执行遗留的临时目标；
# execute-as 对每个 rpg.hurt 实体顺序执行，因此同刻多场战斗也不会串目标。
tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @s add rpg.legacy.target
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.chainsaw_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/chainsaw
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.montain_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/mountain
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.pen_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/pen
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.potion_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/venom
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.soul_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/abaddon
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.ashes_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/ashes_hit
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.power_tag1] run function rpg:item/legacy/throne_mark
tag @s remove rpg.legacy.target
