bossbar set rpg:prologue_zh_i2 name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M03.zh","fallback":"主责备你吧。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i2 name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M03.en","fallback":"The Lord rebuke thee.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i2 33
scoreboard players set #subn rpg_pr_i2 403
execute as @a[tag=rpg.pri2] at @s run playsound rpg:vo.prologue.m03 voice @s ~ ~ ~ 1 1
