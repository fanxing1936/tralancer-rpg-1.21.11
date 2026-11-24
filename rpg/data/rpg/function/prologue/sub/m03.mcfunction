bossbar set rpg:prologue_zh name [{"translate":"rpg.prologue.who.michael.zh","fallback":"米迦勒","color":"#FFD85A","italic":false,"bold":true},{"text":"：","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M03.zh","fallback":"主责备你吧。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en name [{"translate":"rpg.prologue.who.michael.en","fallback":"Michael","color":"#FFD85A","italic":false,"bold":true},{"text":": ","color":"#FFD85A","bold":true},{"translate":"rpg.prologue.M03.en","fallback":"The Lord rebuke thee.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr 33
scoreboard players set #subn rpg_pr 403
execute as @a[tag=rpg.pr] at @s run playsound rpg:vo.prologue.m03 voice @s ~ ~ ~ 1 1
