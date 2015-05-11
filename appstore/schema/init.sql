SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `boss` DEFAULT CHARACTER SET utf8 ;
USE `boss` ;

-- -----------------------------------------------------
-- Table `boss`.`aps_bss_appstore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `boss`.`aps_bss_appstore` ;

CREATE TABLE IF NOT EXISTS `boss`.`aps_bss_appstore` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '应用市场',
  `name` VARCHAR(128) NULL DEFAULT '' COMMENT '市场简介',
  `spider_name` VARCHAR(32) NULL DEFAULT '' COMMENT 'App市场名',
  `url_pattern` VARCHAR(255) NULL DEFAULT '' COMMENT 'App在市场中的URL格式',
  `corp` VARCHAR(128) NULL DEFAULT '',
  `url` VARCHAR(128) NULL DEFAULT '',
  `contactee` VARCHAR(128) NULL DEFAULT '',
  `address` VARCHAR(25) NULL DEFAULT '',
  `memo` TEXT NULL,
  `status` TINYINT NULL DEFAULT 0 COMMENT '状态。0 = 未生效 1 = 已生效 -1 = 删除',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `boss`.`aps_bss_appstore_xpath`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `boss`.`aps_bss_appstore_xpath` ;

CREATE TABLE IF NOT EXISTS `boss`.`aps_bss_appstore_xpath` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `appstore_id` INT(11) NULL DEFAULT 0 COMMENT 'App市场名',
  `crawl_name` VARCHAR(64) NULL DEFAULT '' COMMENT '爬虫名',
  `field_name` VARCHAR(64) NULL DEFAULT '' COMMENT '存储字段名',
  `unit` VARCHAR(45) NULL DEFAULT '' COMMENT '单位，比如万次',
  `xpath` TEXT NULL COMMENT '需要爬的数据的XPATH',
  `text_pattern` VARCHAR(128) NULL DEFAULT '' COMMENT '目标数据显示格式',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `boss`.`aps_bss_competitor_appstore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `boss`.`aps_bss_competitor_appstore` ;

CREATE TABLE IF NOT EXISTS `boss`.`aps_bss_competitor_appstore` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `appstore_id` INT(11) NULL DEFAULT 0 COMMENT 'App市场ID',
  `competitor_id` INT(11) NULL DEFAULT 0 COMMENT '竞品ID',
  `competitor_mark` VARCHAR(64) NULL DEFAULT '' COMMENT '竞品在市场中标识',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 63
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `boss`.`aps_bss_crawl_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `boss`.`aps_bss_crawl_log` ;

CREATE TABLE IF NOT EXISTS `boss`.`aps_bss_crawl_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL COMMENT '抓取日期',
  `appstore_id` INT NOT NULL DEFAULT 0 COMMENT '市场ID',
  `competitor_id` INT NOT NULL DEFAULT 0 COMMENT '竞品ID',
  `name` VARCHAR(45) NULL DEFAULT '',
  `downloads` DECIMAL(11,2) NULL DEFAULT 0 COMMENT '下载次数（万次）',
  `comments` INT(11) NULL DEFAULT 0 COMMENT '评论次数',
  `rate` DECIMAL(7,2) NULL DEFAULT 0 COMMENT '评分',
  `favs` INT(11) NULL DEFAULT 0 COMMENT '赞',
  `middles` INT(11) NULL DEFAULT 0 COMMENT '中评',
  `dislikes` INT(11) NULL DEFAULT 0 COMMENT '踩',
  `last_version` VARCHAR(16) NULL DEFAULT '' COMMENT '版本',
  `last_comment` TEXT NULL COMMENT '评论内容',
  PRIMARY KEY (`id`),
  INDEX `KEY_APPSTORE_COMPETITOR_DATE` (`appstore_id` ASC, `competitor_id` ASC, `date` DESC),
  INDEX `KEY_APPSTORE_DATE` (`appstore_id` ASC, `date` DESC))
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `boss`.`aps_bss_competitor_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `boss`.`aps_bss_competitor_info` ;

CREATE TABLE IF NOT EXISTS `boss`.`aps_bss_competitor_info` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NULL DEFAULT '' COMMENT '竞品名称',
  `desc` TEXT NULL COMMENT '竞品描述',
  `corp` VARCHAR(128) NULL DEFAULT '' COMMENT '厂家',
  `url` VARCHAR(128) NULL DEFAULT '' COMMENT '网址',
  `contactee` VARCHAR(128) NULL DEFAULT '' COMMENT '联系人',
  `address` VARCHAR(255) NULL DEFAULT '' COMMENT '地址',
  `memo` TEXT NULL COMMENT '备注',
  `status` TINYINT NULL DEFAULT 0 COMMENT '状态。0 = 未生效 1 = 已生效 -1 = 删除',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 63
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `boss`.`aps_bss_appstore`
-- -----------------------------------------------------
START TRANSACTION;
USE `boss`;
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (1, '360手机助手', 'appstore360', 'http://zhushou.360.cn/detail/index/soft_id/{id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (2, '百度手机助手', 'appstorebaidu', 'http://shouji.baidu.com/soft/item?docid={id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (3, '应用宝', 'appstoremyapp', 'http://android.myapp.com/myapp/detail.htm?apkName={id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (4, '豌豆荚', 'appstorewandoujia', 'http://www.wandoujia.com/apps/{id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (5, '安卓市场', 'appstorehiapk', 'http://apk.hiapk.com/appinfo/{id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (6, '91市场', 'appstore91', 'http://apk.91.com/Soft/Android/{id}.html', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (7, '华为应用市场', 'appstorevmall', 'http://app.vmall.com/app/{id}', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_appstore` (`id`, `name`, `spider_name`, `url_pattern`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (8, '联想乐商店', 'appstorelenovo', 'http://app.lenovo.com/app/{id}.html', '', '', '', '', '', 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `boss`.`aps_bss_competitor_appstore`
-- -----------------------------------------------------
START TRANSACTION;
USE `boss`;
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (1, 1, 1, '125213');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (2, 1, 2, '841182');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (3, 1, 3, '155167');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (4, 1, 4, '72852');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (5, 1, 5, '525578');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (6, 1, 6, '118651');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (7, 1, 7, '98095');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (8, 1, 8, '708727');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (9, 1, 9, '198622');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (10, 2, 1, '6722489');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (11, 2, 2, '6828600');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (12, 2, 3, '6822756');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (13, 2, 4, '6789888');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (14, 2, 5, '6827852');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (15, 2, 6, '6828397');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (16, 2, 7, '6654357');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (17, 2, 8, '6793181');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (18, 2, 9, '6809263');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (19, 3, 1, 'com.appshare.android.ilisten');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (20, 3, 2, 'com.duoduo.child.story');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (21, 3, 3, 'com.xiaobanlong.main');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (22, 3, 4, 'com.kunpeng.babyting');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (23, 3, 5, 'com.slanissue.apps.mobile.erge');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (24, 3, 6, 'com.iflytek.hipanda');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (25, 3, 7, 'com.babytree.apps.pregnancy');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (26, 3, 8, 'dianyun.baobaowd');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (27, 3, 9, 'com.dw.btime');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (28, 4, 1, 'com.appshare.android.ilisten');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (29, 4, 2, 'com.duoduo.child.story');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (30, 4, 3, 'com.xiaobanlong.main');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (31, 4, 4, 'com.kunpeng.babyting');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (32, 4, 5, 'com.slanissue.apps.mobile.erge');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (33, 4, 6, 'com.iflytek.hipanda');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (34, 4, 7, 'com.babytree.apps.pregnancy');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (35, 4, 8, 'dianyun.baobaowd');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (36, 4, 9, 'com.dw.btime');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (37, 5, 1, 'com.appshare.android.ilisten');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (38, 5, 2, 'com.duoduo.child.story');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (39, 5, 3, 'com.xiaobanlong.main');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (40, 5, 4, 'com.kunpeng.babyting');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (41, 5, 5, 'com.slanissue.apps.mobile.erge');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (42, 5, 6, 'com.iflytek.hipanda');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (43, 5, 7, 'com.babytree.apps.pregnancy');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (44, 5, 8, 'dianyun.baobaowd');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (45, 5, 9, 'com.dw.btime');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (46, 6, 1, 'com.appshare.android.ilisten');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (47, 6, 2, 'com.duoduo.child.story');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (48, 6, 3, 'com.xiaobanlong.main');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (49, 6, 4, 'com.kunpeng.babyting');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (50, 6, 5, 'com.slanissue.apps.mobile.erge');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (51, 6, 6, 'com.iflytek.hipanda');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (52, 6, 7, 'com.babytree.apps.pregnancy');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (53, 6, 8, 'dianyun.baobaowd');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (54, 6, 9, 'com.dw.btime');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (55, 7, 1, 'C55044');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (56, 7, 2, 'C10087276');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (57, 7, 3, 'SC67132');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (58, 7, 4, 'C34509');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (59, 7, 5, 'C10083662');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (60, 7, 6, 'SC57048');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (61, 7, 7, 'C43237');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (62, 7, 8, 'C10061154');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (63, 7, 9, 'C191426');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (64, 8, 1, '15180324');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (65, 8, 2, '15259140');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (66, 8, 3, '15248582');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (67, 8, 4, '15224930');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (68, 8, 5, '15258923');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (69, 8, 6, '15258977');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (70, 8, 7, '15053783');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (71, 8, 8, '15231732');
INSERT INTO `boss`.`aps_bss_competitor_appstore` (`id`, `appstore_id`, `competitor_id`, `competitor_mark`) VALUES (72, 8, 9, '15243197');

COMMIT;


-- -----------------------------------------------------
-- Data for table `boss`.`aps_bss_competitor_info`
-- -----------------------------------------------------
START TRANSACTION;
USE `boss`;
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (1, '口袋故事听听', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (2, '儿歌多多', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (3, '小伴龙', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (4, '宝贝听听', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (5, '贝瓦儿歌', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (6, '开心熊宝', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (7, '快乐孕期', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (8, '柚柚育儿', '', '', '', '', '', '', 1);
INSERT INTO `boss`.`aps_bss_competitor_info` (`id`, `name`, `desc`, `corp`, `url`, `contactee`, `address`, `memo`, `status`) VALUES (9, '亲宝宝-育儿怀孕', '', '', '', '', '', '', 1);

COMMIT;

