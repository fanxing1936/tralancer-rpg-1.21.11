scoreboard objectives add rpg_pr_i1 dummy
scoreboard objectives add rpg_pr_role dummy
scoreboard objectives add rpg_pr_id dummy
scoreboard objectives add rpg_pr_cd1 dummy
scoreboard objectives add rpg_pr_cd2 dummy
scoreboard objectives add rpg_pr_av dummy
scoreboard objectives add rpg_pr_down dummy
scoreboard objectives add rpg_pr_done dummy
scoreboard objectives add rpg_pr_lv minecraft.custom:minecraft.leave_game
scoreboard players set #ten rpg_pr_i1 10
scoreboard players set #hund rpg_pr_i1 100
scoreboard players set #twenty rpg_pr_i1 20
scoreboard objectives add rpg_pr_s1 dummy
scoreboard objectives add rpg_pr_s2 dummy
execute unless score #state rpg_pr_i1 matches 0.. run scoreboard players set #state rpg_pr_i1 0
bossbar add rpg:prologue_zh_i1 ""
bossbar add rpg:prologue_en_i1 ""
bossbar set rpg:prologue_zh_i1 color pink
bossbar set rpg:prologue_en_i1 color pink
bossbar set rpg:prologue_zh_i1 visible false
bossbar set rpg:prologue_en_i1 visible false
