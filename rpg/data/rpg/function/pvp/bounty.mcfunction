advancement revoke @s only rpg:pvp/bounty
execute unless entity @s[tag=rpg.ch] run return 0
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
scoreboard players add @s rpg_tl_ch 10
tellraw @a ["",{"text":"〖通缉令〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"selector":"@s","color":"#E6DFCF"},{"text":" 拿下了一名暴露的恶魔信徒，领了教廷的赏。","color":"#9C9A94","bold":false,"italic":false}]
