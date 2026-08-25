tag @s add rpg.ch1.witness.ready
tag @s add rpg.ch1.witness.controller
execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.witness.controller,limit=1] rpg_ch1_id run function rpg:campaign/beelzebub/witness/confirm_player
tag @s remove rpg.ch1.witness.controller
tellraw @a[tag=rpg.ch1.current,distance=..72] ["",{"text":"[真名确证] ","color":"#D4AF37","bold":true,"italic":false},{"text":"三种不可重复的权能已被见证；现实承认别西卜来过。","color":"#B5D957","bold":false,"italic":false}]
