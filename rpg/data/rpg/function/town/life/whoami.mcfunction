# 说话的是谁（as 那位）
execute if entity @s[tag=rpg.tnpc.priest] run scoreboard players set #role rpg_tl 1
execute if entity @s[tag=rpg.tnpc.elder] run scoreboard players set #role rpg_tl 2
execute if entity @s[tag=rpg.tnpc.bard] run scoreboard players set #role rpg_tl 3
execute if entity @s[tag=rpg.tnpc.watchman] run scoreboard players set #role rpg_tl 4
execute if entity @s[tag=rpg.tnpc.child] run scoreboard players set #role rpg_tl 5
execute if entity @s[tag=rpg.tnpc.board] run scoreboard players set #role rpg_tl 6
execute if entity @s[tag=rpg.tnpc.folk] run scoreboard players set #role rpg_tl 7
scoreboard players operation #t rpg_tl = @s rpg_tw_id
execute if entity @s[tag=rpg.tnpc.farmwife] run scoreboard players set #folk rpg_tl 1
execute if entity @s[tag=rpg.tnpc.farmer] run scoreboard players set #folk rpg_tl 2
execute if entity @s[tag=rpg.tnpc.lad] run scoreboard players set #folk rpg_tl 3
execute if entity @s[type=minecraft:villager] run rotate @s facing entity @p[distance=..8]
execute if entity @s[tag=rpg.tnpc.hood] run scoreboard players set #role rpg_tl 8
execute if entity @s[tag=rpg.tnpc.witch] run scoreboard players set #role rpg_tl 9
execute if entity @s[tag=rpg.tnpc.altar] run scoreboard players set #role rpg_tl 10
