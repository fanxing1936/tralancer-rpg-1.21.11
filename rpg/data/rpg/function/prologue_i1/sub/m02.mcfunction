bossbar set rpg:prologue_zh_i1 name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M02.zh","fallback":"路西法，你本是无所不备的，智慧充足，全然美丽。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i1 name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M02.en","fallback":"Lucifer — thou sealest up the sum, full of wisdom, and perfect in beauty.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i1 96
scoreboard players set #subn rpg_pr_i1 402
execute as @a[tag=rpg.pri1] at @s run playsound rpg:vo.prologue.m02 voice @s ~ ~ ~ 1 1
