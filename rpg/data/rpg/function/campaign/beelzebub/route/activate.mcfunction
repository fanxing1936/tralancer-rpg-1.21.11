scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_choice 0
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"路线密文｜按因果顺序重排三份记录","color":"#B8A98B","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[路线密文] ","color":"#B8A98B","bold":true,"italic":false},{"text":"按‘行动起点 → 被害者名册 → 最终目的地’依次踏入三枚证物。错误排序会唤来食名蝇。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/route/spawn_choices
