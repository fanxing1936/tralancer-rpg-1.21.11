bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.who.lucifer.zh","fallback":"路西法","color":"#F2E6B8","italic":false,"bold":true},{"text":"：","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D03.zh","fallback":"那就从他身上踏过去。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.who.lucifer.en","fallback":"Lucifer","color":"#F2E6B8","italic":false,"bold":true},{"text":": ","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D03.en","fallback":"Then we walk over him.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i3 44
scoreboard players set #subn rpg_pr_i3 303
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.d03 voice @s ~ ~ ~ 1 1
