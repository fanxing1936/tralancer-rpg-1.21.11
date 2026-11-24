bossbar set rpg:prologue_zh name [{"translate":"rpg.prologue.who.lucifer.zh","fallback":"路西法","color":"#F2E6B8","italic":false,"bold":true},{"text":"：","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D03.zh","fallback":"那就从他身上踏过去。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en name [{"translate":"rpg.prologue.who.lucifer.en","fallback":"Lucifer","color":"#F2E6B8","italic":false,"bold":true},{"text":": ","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D03.en","fallback":"Then we walk over him.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr 44
scoreboard players set #subn rpg_pr 303
execute as @a[tag=rpg.pr] at @s run playsound rpg:vo.prologue.d03 voice @s ~ ~ ~ 1 1
