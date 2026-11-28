bossbar set rpg:prologue_zh_i1 name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.X02.zh","fallback":"那一天要到来了。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i1 name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.X02.en","fallback":"That day is coming.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i1 43
scoreboard players set #subn rpg_pr_i1 702
execute as @a[tag=rpg.pri1] at @s run playsound rpg:vo.prologue.x02 voice @s ~ ~ ~ 1 1
