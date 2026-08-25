tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.cleanup.controller
tag @a remove rpg.ch1.cleanup.player
execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.cleanup.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup.player
tag @e[tag=rpg.ch1.scene,distance=..72] remove rpg.ch1.cleanup
execute as @e[tag=rpg.ch1.scene,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup
tag @e[tag=rpg.ch1.minion,distance=..72] remove rpg.ch1.cleanup
execute as @e[tag=rpg.ch1.minion,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup
tag @e[tag=rpg.ch1.boss,distance=..72] remove rpg.ch1.cleanup
execute as @e[tag=rpg.ch1.boss,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.cleanup
execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.accepted
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.member
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.party
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.host
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.current
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.kit.issued
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.career.confirmed
scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_id 0
scoreboard players set @a[tag=rpg.ch1.cleanup.player] rpg_ch1_session 0
tag @a[tag=rpg.ch1.cleanup.player] remove rpg.ch1.cleanup.player
bossbar remove rpg:chapter1
kill @e[tag=rpg.ch1.cleanup,distance=..72]
