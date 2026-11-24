bossbar set rpg:prologue_zh name [{"translate":"rpg.prologue.who.beelzebub.zh","fallback":"别西卜","color":"#B5D957","italic":false,"bold":true},{"text":"：","color":"#B5D957","bold":true},{"translate":"rpg.prologue.D02.zh","fallback":"米迦勒就在前面。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en name [{"translate":"rpg.prologue.who.beelzebub.en","fallback":"Beelzebub","color":"#B5D957","italic":false,"bold":true},{"text":": ","color":"#B5D957","bold":true},{"translate":"rpg.prologue.D02.en","fallback":"Michael is just ahead.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr 44
scoreboard players set #subn rpg_pr 302
execute as @a[tag=rpg.pr] at @s run playsound rpg:vo.prologue.d02 voice @s ~ ~ ~ 1 1
