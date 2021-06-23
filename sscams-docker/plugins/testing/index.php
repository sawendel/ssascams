<?php

class TestingPlugin extends \RainLoop\Plugins\AbstractPlugin
{
	
	public function Init()
	{
		$this->addJs('js/testing.js');

		// $this->addHook('ajax.action-pre-call', 'AjaxActionPreCall');
		// $this->addHook('filter.ajax-response', 'FilterAjaxResponse');
	}

	
}
