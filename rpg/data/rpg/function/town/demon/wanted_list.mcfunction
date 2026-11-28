tag @s add rpg.dm.reader
tellraw @s ["",{"text":"〖通缉令〗","color":"#C9A646","bold":true,"italic":false},{"text":"  教廷悬赏捉拿以下暴露的恶魔信徒：","color":"#9C9A94","bold":false,"italic":false}]
execute unless entity @a[scores={rpg_dm_exp=1..}] run tellraw @s ["",{"text":"　（眼下没有）","color":"#797979","bold":false,"italic":false}]
execute as @a[scores={rpg_dm_exp=1..}] run tellraw @a[tag=rpg.dm.reader] ["",{"text":"　","color":"#9C9A94","bold":false,"italic":false},{"selector":"@s","color":"#A276BE"},{"text":"　还剩 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_dm_exp"},"color":"#E6DFCF"},{"text":" 秒","color":"#9C9A94","bold":false,"italic":false}]
tag @s remove rpg.dm.reader
