bossbar set rpg:prologue_zh_i2 name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M01.zh","fallback":"谁似神！","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i2 name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M01.en","fallback":"Who is like God!","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i2 32
scoreboard players set #subn rpg_pr_i2 401
execute as @a[tag=rpg.pri2] at @s run playsound rpg:vo.prologue.m01 voice @s ~ ~ ~ 1 1
