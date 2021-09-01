DROP PROCEDURE IF EXISTS sscams_registermailbox;
DELIMITER $$

CREATE PROCEDURE sscams_registermailbox
(
	pEmail VARCHAR(255),
    pFullName VARCHAR(255)
)
BEGIN
	-- crear un sistema de código errores 
	DECLARE SUCCEED INT DEFAULT(53000);
	DECLARE INTERNAL_FAILED INT DEFAULT(53001);
	DECLARE EMAIL_ALREADY_EXISTS INT DEFAULT(53002);

	DECLARE domainName VARCHAR(100);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		GET DIAGNOSTICS CONDITION 1 @err_no = MYSQL_ERRNO, @message = MESSAGE_TEXT;
        
        IF (ISNULL(@message)) THEN 
			SET @message = 'Problem with email creation, check error code number';            
        ELSE
            SET @message = CONCAT('Internal error: ', @message);
        END IF;
        
        ROLLBACK;
        
        RESIGNAL SET MESSAGE_TEXT = @message;
	END;

	SET autocommit = 0;

	IF EXISTS(SELECT username FROM mailbox WHERE username=pEmail) THEN 
		SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO = EMAIL_ALREADY_EXISTS;		
	END IF;

	SET domainName = TRIM(SUBSTRING(pEmail, LOCATE('@', pEmail)+1));

	START TRANSACTION;
		INSERT INTO mailbox (username, password, name,
                     storagebasedirectory,storagenode, maildir,
                     quota, domain, active, passwordlastchange, created)
		SELECT pEmail, password, pFullName,
		storagebasedirectory,  storagenode, CONCAT(domainName, '/t/r/s/', UUID()),
		quota, domain, active, NOW(), NOW() FROM
		mailbox where username=CONCAT('template@', domainName);

		INSERT INTO forwardings (address, forwarding, domain, dest_domain, is_forwarding)
        VALUES (pEmail, pEmail, domainName, domainName, 1);

    COMMIT;
END$$
DELIMITER ;


CREATE TABLE IF NOT EXISTS `vmail`.`scams_emailsents` (
  `sentid` BIGINT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100),
  `posttime` DATETIME NOT NULL,
  `campaingid` BIGINT NOT NULL,
  `templateid` BIGINT NOT NULL,
  PRIMARY KEY (`sentid`)
)
ENGINE = InnoDB
AUTO_INCREMENT = 1;


DROP PROCEDURE IF EXISTS sscams_checkduplicate;
DELIMITER $$

CREATE PROCEDURE sscams_checkduplicate(
	pEmail VARCHAR(100), 
	pCampaingid BIGINT, 
	pTemplateid BIGINT
) 
BEGIN
	DECLARE DUPLICATED INT DEFAULT(1);
	DECLARE NEWEMAIL INT DEFAULT(0);

	IF EXISTS(SELECT sentid FROM scams_emailsents 
		WHERE email=pEmail 
		AND campaingid=pCampaingid AND templateid=pTemplateid )
	THEN
		SELECT DUPLICATED AS duplicated;
	ELSE
		INSERT INTO scams_emailsents(email, posttime, campaingid, templateid)
		VALUES
		(pEmail, NOW(), pCampaingid, pTemplateid);

		SELECT NEWEMAIL AS duplicated;
	END IF ;
END $$
DELIMITER ;


CREATE TABLE IF NOT EXISTS `vmail`.`groups_per_campaign` (
  `groupid` BIGINT NOT NULL,
  `groupname` VARCHAR(100) NOT NULL,
  `campaignid` BIGINT NOT NULL,
  `campaignname` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`groupid`, `campaignid`)
)
ENGINE = InnoDB
AUTO_INCREMENT = 1;





CREATE TABLE IF NOT EXISTS `vmail`.`sscams_groupstosend` (
  groupname VARCHAR(120) NOT NULL,
  sendit SMALLINT NOT NULL DEFAULT(0)
)
ENGINE = InnoDB;

DROP PROCEDURE IF EXISTS lunchmailgroup;

DELIMITER //

CREATE PROCEDURE lunchmailgroup(pGroupName VARCHAR(120))
BEGIN 
	DECLARE groupfound VARCHAR(120);
    SET groupfound = NULL;
    
    START TRANSACTION;
		SELECT groupname INTO groupfound FROM sscams_groupstosend WHERE groupname = pGroupName;
		
		IF ISNULL(groupfound) THEN
			INSERT INTO sscams_groupstosend (groupname, sendit) VALUES (pGroupName, 1);
		ELSE
			UPDATE sscams_groupstosend SET sendit = 1 WHERE groupname = pGroupName;
		END IF;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS checkgroupstosend //

CREATE PROCEDURE checkgroupstosend()
BEGIN 
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		DROP TEMPORARY TABLE groupstosend;
	END;
    
	START TRANSACTION;
		CREATE TEMPORARY TABLE groupstosend
		SELECT groupname FROM sscams_groupstosend WHERE sendit = 1;

		UPDATE sscams_groupstosend SET sendit = 0 WHERE groupname IN (SELECT groupname FROM groupstosend);
		
		SELECT DISTINCT tosend.groupname, camp.campaignid FROM groupstosend tosend 
        INNER JOIN groups_per_campaign camp ON TRIM(camp.groupname) = TRIM(tosend.groupname);
		
	COMMIT;
END //

DELIMITER ;