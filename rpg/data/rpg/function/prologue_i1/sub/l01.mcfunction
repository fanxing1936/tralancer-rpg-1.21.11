bossbar set rpg:prologue_zh_i1 name [{"translate":"rpg.prologue.who.lucifer.zh","fallback":"路西法","color":"#F2E6B8","italic":false,"bold":true},{"text":"：","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.L01.zh","fallback":"散开！","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i1 name [{"translate":"rpg.prologue.who.lucifer.en","fallback":"Lucifer","color":"#F2E6B8","italic":false,"bold":true},{"text":": ","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.L01.en","fallback":"Scatter!","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i1 25
scoreboard players set #subn rpg_pr_i1 501
execute as @a[tag=rpg.pri1] at @s run playsound rpg:vo.prologue.l01 voice @s ~ ~ ~ 1 1
