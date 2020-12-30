; This is in the "rando" namespace.
;
; The data in this file will be modified by the randomizer. (It should not modify the collect mode,
; only the treasure object.)
;
; Data Format:
;   dwbe <Treasure Object Index>
;   .db <Collect Mode>
;   .dw <Function to run upon getting the item, or $0000>
;
; Misc notes:
; - COLLECT_MODE_FALL will be changed to COLLECT_MODE_FALL_KEY if the item in the slot is a small
;   key (uses "TREASURE_COLLECT_MODE_NO_CHANGE"). Also, the key won't have its text shown. This is
;   done in the disassembly code.


.ifdef ROM_SEASONS

seasonsSlot_makuTree:
	dwbe TREASURE_OBJECT_GNARLED_KEY_00
	.db  COLLECT_MODE_FALL
	.dw  seasonsSlotCallback_makuTree

seasonsSlot_shop150Rupees:
	dwbe TREASURE_OBJECT_FLUTE_00
	.db  $00
	.dw  $0000

seasonsSlot_membersShop1:
	dwbe TREASURE_OBJECT_SEED_SATCHEL_00
	.db  $00
	.dw  $0000

seasonsSlot_membersShop2:
	dwbe TREASURE_OBJECT_GASHA_SEED_00
	.db  $00
	.dw  $0000

seasonsSlot_membersShop3:
	dwbe TREASURE_OBJECT_TREASURE_MAP_00
	.db  $00
	.dw  $0000

seasonsSlot_subrosianDanceHall:
	dwbe TREASURE_OBJECT_BOOMERANG_00
	.db  COLLECT_MODE_PICKUP_2HAND
	.dw  $0000


seasonsSlot_d0KeyChest:
	dwbe TREASURE_OBJECT_SMALL_KEY_03
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d0SwordChest:
	dwbe TREASURE_OBJECT_SWORD_00
	.db  $00
	.dw  $0000

seasonsSlot_d0RupeeChest:
	dwbe TREASURE_OBJECT_RUPEES_04
	.db  COLLECT_MODE_CHEST
	.dw  $0000


seasonsSlot_d1_stalfosDrop:
	dwbe TREASURE_OBJECT_SMALL_KEY_03
	.db  COLLECT_MODE_FALL
	.dw  $0000

seasonsSlot_d1_stalfosChest:
	dwbe TREASURE_OBJECT_MAP_02
	.db  COLLECT_MODE_CHEST_MAP_OR_COMPASS
	.dw  $0000

seasonsSlot_d1_blockPushingRoom:
	dwbe TREASURE_OBJECT_GASHA_SEED_01
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d1_leverRoom:
	dwbe TREASURE_OBJECT_COMPASS_02
	.db  COLLECT_MODE_CHEST_MAP_OR_COMPASS
	.dw  $0000

seasonsSlot_d1_railwayChest:
	dwbe TREASURE_OBJECT_BOMBS_00
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d1_buttonChest:
	dwbe TREASURE_OBJECT_SMALL_KEY_03
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d1_basement:
	dwbe TREASURE_OBJECT_SEED_SATCHEL_00
	.db  COLLECT_MODE_PICKUP_2HAND
	.dw  $0000

seasonsSlot_d1_goriyaChest:
	dwbe TREASURE_OBJECT_BOSS_KEY_03
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d1_floormasterRoom:
	dwbe TREASURE_OBJECT_RING_04
	.db  COLLECT_MODE_CHEST
	.dw  $0000

seasonsSlot_d1_boss:
	dwbe TREASURE_OBJECT_HEART_CONTAINER_00
	.db  COLLECT_MODE_POOF
	.dw  $0000

.endif