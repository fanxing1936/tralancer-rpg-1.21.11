scoreboard players set @s rpg_q1 99
function rpg:quest/q1_pick
bossbar set rpg:quest_sub name ["",{"text":"〔支线・铁匠的遗嘱〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"老铁匠留下的图纸，现在归你了。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・铁匠的遗嘱〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔖𝔪𝔦𝔱𝔥'𝔰 𝔚𝔦𝔩𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  老铁匠留下的图纸，现在归你了。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
