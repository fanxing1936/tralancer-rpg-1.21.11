execute as @a[tag=rpg.ch1.current,tag=!rpg.ch1.kit.issued] run function rpg:campaign/beelzebub/cache/reissue_missing
tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss] remove rpg.ch1.boss.current
execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,tag=!rpg.ch1.rite,distance=..64] at @s if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,distance=..14,limit=1] run function rpg:campaign/beelzebub/claim_rite
execute if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,scores={rpg_ex_stage=0},limit=1] run bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅰ 镇压 · 亲历三种不同权能","color":"#5A6B1E","bold":true,"italic":false}]
execute if entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,scores={rpg_ex_stage=1},limit=1] run bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅱ 镇魔 · 真名 + 点燃图腾","color":"#D4AF37","bold":true,"italic":false}]
execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=2},limit=1] run bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅲ 固阵 · 稳定度推进至 100","color":"#62D9E8","bold":true,"italic":false}]
execute if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,scores={rpg_ex_stage=4},limit=1] run bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅳ 裁决 · 四选一","color":"#D596F2","bold":true,"italic":false}]
execute if score @s rpg_ch1_time matches 140 run tellraw @a[tag=rpg.ch1.current] ["",{"text":"[见证规则] ","color":"#D4AF37","bold":true,"italic":false},{"text":"环境证物只是推论；亲历三种不同招式后，现实才承认真名。","color":"gray","bold":false,"italic":false}]
execute unless entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,limit=1] if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/recover_boss
