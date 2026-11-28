bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.who.antichrist.zh","fallback":"敌基督","color":"#8B1A1A","italic":false,"bold":true},{"text":"：","color":"#8B1A1A","bold":true},{"translate":"rpg.prologue.X01.zh","fallback":"我会回来的。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.who.antichrist.en","fallback":"The Antichrist","color":"#8B1A1A","italic":false,"bold":true},{"text":": ","color":"#8B1A1A","bold":true},{"translate":"rpg.prologue.X01.en","fallback":"I will return.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i3 53
scoreboard players set #subn rpg_pr_i3 701
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.x01 voice @s ~ ~ ~ 1 1
