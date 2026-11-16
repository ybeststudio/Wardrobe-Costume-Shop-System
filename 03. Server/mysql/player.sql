CREATE TABLE IF NOT EXISTS `wardrobe_state` (
  `pid` int(10) unsigned NOT NULL,
  `look0` int(10) unsigned NOT NULL DEFAULT 0,
  `look1` int(10) unsigned NOT NULL DEFAULT 0,
  `look2` int(10) unsigned NOT NULL DEFAULT 0,
  `look3` int(10) unsigned NOT NULL DEFAULT 0,
  `look4` int(10) unsigned NOT NULL DEFAULT 0,
  `look5` int(10) unsigned NOT NULL DEFAULT 0,
  `look6` int(10) unsigned NOT NULL DEFAULT 0,
  `look7` int(10) unsigned NOT NULL DEFAULT 0,
  `look8` int(10) unsigned NOT NULL DEFAULT 0,
  `remembered` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `applied` tinyint(3) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE IF NOT EXISTS `wardrobe_outfit` (
  `pid` int(10) unsigned NOT NULL,
  `slot` tinyint(3) unsigned NOT NULL,
  `revision` int(10) unsigned NOT NULL DEFAULT 0,
  `used` tinyint(4) NOT NULL DEFAULT 0,
  `name` varchar(96) NOT NULL DEFAULT '',
  `look0` int(10) unsigned NOT NULL DEFAULT 0,
  `look1` int(10) unsigned NOT NULL DEFAULT 0,
  `look2` int(10) unsigned NOT NULL DEFAULT 0,
  `look3` int(10) unsigned NOT NULL DEFAULT 0,
  `look4` int(10) unsigned NOT NULL DEFAULT 0,
  `look5` int(10) unsigned NOT NULL DEFAULT 0,
  `look6` int(10) unsigned NOT NULL DEFAULT 0,
  `look7` int(10) unsigned NOT NULL DEFAULT 0,
  `look8` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`,`slot`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- item.window enum'una 'WARDROBE' ekle (mevcut degerlerin sonuna). Ornek:
-- ALTER TABLE `item` MODIFY `window` ENUM('INVENTORY','EQUIPMENT','SAFEBOX','MALL','DRAGON_SOUL_INVENTORY','BELT_INVENTORY','GROUND', ... ,'WARDROBE') NOT NULL;
-- Kendi enum listeni koru, sadece en sona 'WARDROBE' ekle.
