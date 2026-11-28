bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.who.mammon.zh","fallback":"玛门","color":"#E6A23C","italic":false,"bold":true},{"text":"：","color":"#E6A23C","bold":true},{"translate":"rpg.prologue.E03.zh","fallback":"赔本的买卖，我不做。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.who.mammon.en","fallback":"Mammon","color":"#E6A23C","italic":false,"bold":true},{"text":": ","color":"#E6A23C","bold":true},{"translate":"rpg.prologue.E03.en","fallback":"I don't make losing trades.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i3 35
scoreboard players set #subn rpg_pr_i3 603
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.e03 voice @s ~ ~ ~ 1 1
