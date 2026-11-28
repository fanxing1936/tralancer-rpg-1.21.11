bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.who.lucifer.zh","fallback":"路西法","color":"#F2E6B8","italic":false,"bold":true},{"text":"：","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D05.zh","fallback":"归我们。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.who.lucifer.en","fallback":"Lucifer","color":"#F2E6B8","italic":false,"bold":true},{"text":": ","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D05.en","fallback":"Ours.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i3 24
scoreboard players set #subn rpg_pr_i3 305
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.d05 voice @s ~ ~ ~ 1 1
