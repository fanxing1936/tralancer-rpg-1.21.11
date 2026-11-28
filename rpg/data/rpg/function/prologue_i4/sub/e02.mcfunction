bossbar set rpg:prologue_zh_i4 name [{"translate":"rpg.prologue.who.belial.zh","fallback":"贝利尔","color":"#D97AD9","italic":false,"bold":true},{"text":"：","color":"#D97AD9","bold":true},{"translate":"rpg.prologue.E02.zh","fallback":"天上没有值得我死的东西。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.who.belial.en","fallback":"Belial","color":"#D97AD9","italic":false,"bold":true},{"text":": ","color":"#D97AD9","bold":true},{"translate":"rpg.prologue.E02.en","fallback":"There's nothing in Heaven worth dying for.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i4 55
scoreboard players set #subn rpg_pr_i4 602
execute as @a[tag=rpg.pri4] at @s run playsound rpg:vo.prologue.e02 voice @s ~ ~ ~ 1 1
