override fun openLastRead(): Flow<ChapterUI?> =
		flow {
			val array = chaptersFlow.first()
			val sortedArray = array.sortedBy { it.order }
			val result = isChaptersResumeFirstUnread()

			val index: Int = if (!result)
				sortedArray.indexOfFirst { it.readingStatus != ReadingStatus.READ }
			else sortedArray.indexOfFirst { it.readingStatus == ReadingStatus.UNREAD }
			

			emit(
				if (index == -1) {
					null
				} else {
					itemIndex.emit(index + 1) // +1 to account for header
					sortedArray[index]
						}
			)
		}.onIO()
		
		
		
		override fun openLastRead(): Flow<ChapterUI?> =
		flow {
			val array = chaptersFlow.first()
			val sortedArray = array.sortedBy { it.order }
			val result = isChaptersResumeFirstUnread()
			val item = if (!result)
			sortedArray.firstOrNull { it.readingStatus != ReadingStatus.READ }
			else sortedArray.firstOrNull { it.readingStatus == ReadingStatus.UNREAD }
			emit(
			if (item == null) {
					null
				} else {
					itemIndex.emit(array.indexOf(item) + 1) // +1 to account for header
					item
				}
			)
		}.onIO()
