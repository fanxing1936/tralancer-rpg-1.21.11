bossbar set rpg:prologue_zh_i4 name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M04.zh","fallback":"你因美丽心中高傲。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M04.en","fallback":"Thine heart was lifted up because of thy beauty.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i4 59
scoreboard players set #subn rpg_pr_i4 404
execute as @a[tag=rpg.pri4] at @s run playsound rpg:vo.prologue.m04 voice @s ~ ~ ~ 1 1
