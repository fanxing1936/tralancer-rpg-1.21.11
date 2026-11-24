bossbar set rpg:prologue_zh name [{"translate":"rpg.prologue.who.mammon.zh","fallback":"玛门","color":"#E6A23C","italic":false,"bold":true},{"text":"：","color":"#E6A23C","bold":true},{"translate":"rpg.prologue.D06.zh","fallback":"宝库也算在里面。记住你说的。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en name [{"translate":"rpg.prologue.who.mammon.en","fallback":"Mammon","color":"#E6A23C","italic":false,"bold":true},{"text":": ","color":"#E6A23C","bold":true},{"translate":"rpg.prologue.D06.en","fallback":"The treasuries too. Remember you said it.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr 55
scoreboard players set #subn rpg_pr 306
execute as @a[tag=rpg.pr] at @s run playsound rpg:vo.prologue.d06 voice @s ~ ~ ~ 1 1
